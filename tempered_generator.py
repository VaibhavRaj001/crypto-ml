import os
import random
import shutil

SRC = "data/original"
DEST = "data/tampered"

os.makedirs(DEST, exist_ok=True)


def byte_flip(data, flips=10):
    data = bytearray(data)
    for _ in range(flips):
        i = random.randint(0, len(data) - 1)
        data[i] = random.randint(0, 255)
    return data


def append_noise(data, size=100):
    return data + os.urandom(size)


def truncate_data(data, percent=0.1):
    cut = int(len(data) * percent)
    return data[:-cut]


def shuffle_blocks(data, block_size=50):
    blocks = [data[i:i+block_size] for i in range(0, len(data), block_size)]
    random.shuffle(blocks)
    return b"".join(blocks)


def generate_tampered():
    for file in os.listdir(SRC):
        src_path = os.path.join(SRC, file)
        with open(src_path, "rb") as f:
            data = f.read()

        attacks = {
            "flip": byte_flip(data),
            "append": append_noise(data),
            "truncate": truncate_data(data),
            "shuffle": shuffle_blocks(data),
        }

        for attack, new_data in attacks.items():
            name = f"{file}_{attack}"
            dest_path = os.path.join(DEST, name)
            with open(dest_path, "wb") as f:
                f.write(new_data)

    print("✅ Advanced tampered dataset generated")


if __name__ == "__main__":
    generate_tampered()
