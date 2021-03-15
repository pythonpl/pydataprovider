import asyncio
import sys
from asyncua import ua, Server

from MachineModel import Model as ElectricModel

global motors
global opcVariables

async def dataExchange():
    for index, motor in enumerate(motors):
        variableName = "motor" + str(index) + "_param"
        await opcVariables[variableName].write_value(motors[index].getParameter())
        variableName = "motor" + str(index) + "_start"
        start = await opcVariables[variableName].read_value()
        if start:
            motors[index].start()
        else:
            motors[index].stop()


async def opcProvider():
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://0.0.0.0:9000/')

    uri = 'data.provider'
    idx = await server.register_namespace(uri)

    for index, motor in enumerate(motors):
        motor = 'motor' + str(index)
        motorobj = await server.nodes.objects.add_object(idx, motor)
        variableName = motor + "_param"
        opcVariables[variableName] = await motorobj.add_variable(idx, variableName, 0.0)
        variableName = motor + "_start"
        opcVariables[variableName] = await motorobj.add_variable(idx, variableName,  False)
        await opcVariables[variableName].set_writable()

    print('Server started!', flush=True)

    async with server:
        while True:        
            await asyncio.sleep(1)
            await dataExchange()
           
async def updateMotor(motor):
    while True:
        await asyncio.sleep(1)
        motor.tick()



if __name__ == '__main__':
    motors = []
    opcVariables = {}
    loop = asyncio.get_event_loop()

    motor1 = ElectricModel()
    loop.create_task(updateMotor(motor1))
    motors.append(motor1)

    motor2 = ElectricModel()
    loop.create_task(updateMotor(motor2))
    motors.append(motor2)

    loop.create_task(opcProvider())
    loop.run_forever()
