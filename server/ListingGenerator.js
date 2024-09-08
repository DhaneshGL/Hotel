const { PrismaClient } = require("@prisma/client");
const { faker } = require("@faker-js/faker");
const { categories, types, facilities } = require("./data");

const prisma = new PrismaClient();

const ListingGenerator = async () => {
  try {
    const users = await prisma.user.findMany({
      select: { id: true },
    });

    if (users.length === 0) {
      console.log("No users found. Generate users first.");
      return;
    }

    const listings = [];
    for (let i = 0; i < 10; i++) {
      const randomUserIndex = Math.floor(Math.random() * users.length);
      const randomCategory =
        categories[Math.floor(Math.random() * categories.length)];
      const randomType = types[Math.floor(Math.random() * types.length)];
      const randomFacilities = facilities
        .sort(() => 0.5 - Math.random())
        .slice(0, 2)
        .map((facility) => facility.name);

      const listing = {
        creatorId: users[randomUserIndex].id,
        category: randomCategory.label,
        type: randomType.name,
        streetAddress: faker.location.streetAddress(),
        aptSuite: faker.location.secondaryAddress(),
        city: faker.location.city(),
        province: faker.location.street(),
        country: faker.location.country(),
        guestCount: faker.number.int({ min: 1, max: 10 }),
        bedroomCount: faker.number.int({ min: 1, max: 5 }),
        bedCount: faker.number.int({ min: 1, max: 5 }),
        bathroomCount: faker.number.int({ min: 1, max: 3 }),
        amenities: randomFacilities,
        listingPhotoPaths: [
          faker.image.city(640, 480, true),
          faker.image.city(640, 480, true),
        ],
        title: faker.company.catchPhrase(),
        description: faker.lorem.paragraph(),
        highlight: faker.company.bs(),
        highlightDesc: faker.lorem.sentence(),
        price: parseFloat(faker.commerce.price()),
      };
      listings.push(listing);
    }

    await prisma.listing.createMany({
      data: listings,
    });

    console.log("Fake listings generation complete.");
  } catch (error) {
    console.error("Error seeding fake listings:", error);
  } finally {
    await prisma.$disconnect();
  }
};

module.exports = ListingGenerator;
