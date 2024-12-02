def change(n):
    change = []
    amounts = (100,50,20,10,5,1,0.25,0.1,0.05,0.01)
    for i in range(len(amounts)):
        if n//amounts[i] > 0 and n//amounts[i] % 1 == 0:
            change.append(int(n//amounts[i]))
            if n > 100:
                n%= amounts[i]
                n+=0.01
            else:
                n %= amounts[i]
        else:
            change.append(0)
    return change

print(change(72))




a = [
"# Relevant Variables and their Values:",
"# result = 0.30000000000000004",
"# fraction_result = 6007199254740993/20000000000000000 (or a simplified fraction if possible)"
]

def change_a(s):
    for i in range(len(s)):
        s[i] = s[i][2:]
    return s

print(change_a(a))