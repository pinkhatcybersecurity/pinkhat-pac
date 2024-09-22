# https://peps.python.org/pep-0572/
(z := (y := (x := 0)))
(x := 1, 2)  # Sets x to 1
if env_base := os.environ.get("PYTHONUSERBASE", None):
    return env_base
if self._is_special and (ans := self._check_nans(context=context)):
    return ans
if reductor := dispatch_table.get(cls):
    rv = reductor(x)
elif reductor := getattr(x, "__reduce_ex__", None):
    rv = reductor(4)
elif reductor := getattr(x, "__reduce__", None):
    rv = reductor()
else:
    raise Error("un(deep)copyable object of type %s" % cls)

# Simplifying list comprehensions
stuff = [[y := f(x), x / y] for x in range(5)]

# Loop-and-a-half
while (command := input("> ")) != "quit":
    print("You entered:", command)
