import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class MyAgent(Agent):
    class MyBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"Message received: {msg.body}")
                reply = Message(to=str(msg.sender))
                reply.body = "I received your message!"
                await self.send(reply)

    async def setup(self):
        behaviour = self.MyBehaviour()
        self.add_behaviour(behaviour)


async def main():
    agent = MyAgent("agent@localhost", "password")
    await agent.start()

if __name__ == "__main__":
    spade.run(main())
