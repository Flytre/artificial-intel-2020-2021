import sys; args = sys.argv[1:]
idx = int(args[0]) - 30

myRegexLst = [
    r"/^0$|^10[01]$/",
    r"/^[01]*$/",
    r"/^[01]*0$/",
    r"/[a-z]*[aeiou][a-z]*[aeiou]+[a-z]*/i",
    r"/^0$|^[1][01]*0$/",
    r"/^[01]*110[01]*$/",
    r"/^.{2,4}$/s",
    r"/^ *\d{3} *-? *\d\d *-? *\d{4}$/",
    r"/^.*?\b\w*d\w*\b/im",
    r"/^0[01]*0$|^1[01]*1$|^[01]?$/"
]

if idx < len(myRegexLst):
    print(myRegexLst[idx])
