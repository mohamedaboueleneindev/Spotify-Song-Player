import faker


def generate_valid_email() -> str:
    fake = faker.Faker()
    return fake.email(domain="dev.com")


def generate_valid_password() -> str:
    fake = faker.Faker()
    return fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)


def get_random_display_name() -> str:
    fake = faker.Faker()
    return fake.name()
