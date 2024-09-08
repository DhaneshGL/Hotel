const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

const updateGenerator= async () => {
  try {
    const users = await prisma.user.findMany();

    const listings = await prisma.listing.findMany({
      select: { id: true }
    });

    const listingIds = listings.map(listing => listing.id);

    for (let user of users) {
      const randomIndex = Math.floor(Math.random() * listingIds.length);
      const randomListingId = listingIds[randomIndex];

      await prisma.user.update({
        where: { id: user.id },
        data: {
          propertyList: {
            push: randomListingId
          }
        }
      });
    }

    console.log("Users updated with listing IDs.");
  } catch (error) {
    console.error("Error updating users with listing IDs:", error);
  } finally {
    await prisma.$disconnect();
  }
};

module.exports = updateGenerator;