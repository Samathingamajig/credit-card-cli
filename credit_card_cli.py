import click
import random


def generate_card_number() -> str:
    base = f"{random.randrange(10 ** 15):<015}"
    checksum = calc_checksum(base)
    return f"{base}{checksum}"


def sum_digits(num: int) -> int:
    return sum(int(digit) for digit in str(num))


def calc_checksum(partial_card_number: str) -> int:
    # Luhn algorithm
    # adapted from https://en.wikipedia.org/wiki/Luhn_algorithm
    weighted_sum = 0
    for i, n_str in enumerate(partial_card_number[::-1]):
        weighted_sum += sum_digits(int(n_str) * (2 if i % 2 == 0 else 1))

    return 10 - (weighted_sum % 10)


def verify_checksum(card_number: str) -> bool:
    return calc_checksum(card_number[:-1]) == int(card_number[-1])


@click.group()
def cli():
    pass


@cli.command()
@click.argument("card_number")
def validate(card_number: str):
    # ignore length since non-16 digits is technically allowed
    is_valid = verify_checksum(card_number)
    click.echo("valid" if is_valid else "invalid")
    click.get_current_context().exit(0 if is_valid else 1)


@cli.command()
@click.argument("partial_card_number")
def checksum(partial_card_number: str):
    checksum_val = calc_checksum(partial_card_number)
    click.echo(checksum_val)


@cli.command()
def generate():
    generated_card_number = generate_card_number()
    click.echo(generated_card_number)


if __name__ == "__main__":
    cli()
