import random

scope = "ACGT"
output_dir = "test/"


def generate(length):
    result = ''
    for _ in range(length):
        result += random.choice(scope)
    return result


if __name__ == '__main__':
    basic_length = 10000
    for i in range(1, 16):
        length = basic_length * i
        s1 = generate(basic_length*i)
        s2 = generate(basic_length*i)
        with open(output_dir+f'input{i}.txt', 'w') as f:
            f.write(s1)
            f.write('\n')
            f.write(s2)


