const { PrismaClient } = require('@prisma/client');
const { faker } = require('@faker-js/faker');
const bcrypt = require("bcryptjs");

const prisma = new PrismaClient();

const UserGenerator = async () => {
  const salt = await bcrypt.genSalt();
  const hashedPassword = await bcrypt.hash('password', salt);

  const users = [];
  for (let i = 0; i < 4; i++) {
    const user = {
      firstName: faker.person.firstName(),
      lastName: faker.person.lastName(),
      email: faker.internet.email(),
      password: hashedPassword,
      profileImagePath: faker.image.avatar(),
    };
    users.push(user);
  }

  try {
    await prisma.user.createMany({
      data: users,
    });
    console.log("Fake data generation complete.");
  } catch (error) {
    console.error("Error seeding fake data:", error);
  } finally {
    await prisma.$disconnect();
  }
};

module.exports = UserGenerator;