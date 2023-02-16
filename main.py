
import time
from pkg.prometheus import new_prom
from pkg.agent import init_agent


if __name__ == '__main__':
    try:
        agent = init_agent()
        agent.start()
    except Exception as err:
        print(err)








