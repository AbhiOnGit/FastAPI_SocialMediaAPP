# x = ('apple', 'banana', 'cherry')
# y = enumerate(x)
# for i, p in enumerate(x):
#     print(i,p)

async def get_burgers(number: int):
    burgers = f"{number} Burgers are nice"
    return burgers

async def read_burgers():
    burgers = await get_burgers(2)
    return burgers

read_burgers()