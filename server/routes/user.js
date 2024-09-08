const router = require("express").Router();
const { PrismaClient } = require("@prisma/client");
const prisma = new PrismaClient();

router.get("/:userId/trips", async (req, res) => {
  try {
    const { userId } = req.params;
    const trips = await prisma.booking.findMany({
      where: { customerId: parseInt(userId) },
      include: { customer: true, host: true, listing: true },
    });
    res.status(202).json(trips);
  } catch (err) {
    console.log(err);
    res
      .status(404)
      .json({ message: "Can not find trips!", error: err.message });
  }
});

router.patch("/:userId/:listingId", async (req, res) => {
  try {
    const { userId, listingId } = req.params;

    const user = await prisma.user.findUnique({
      where: { id: parseInt(userId) },
    });

    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }

    const wishList = user.wishList || [];

    if (wishList.includes(listingId)) {
      const updatedWishListIds = wishList.filter((id) => id !== listingId);
      const updatedWishList = await Promise.all(
        updatedWishListIds.map(async (id) => {
          const listing = await prisma.listing.findUnique({
            where: { id: parseInt(id) },
          });
          return listing;
        })
      );

      await prisma.user.update({
        where: { id: parseInt(userId) },
        data: { wishList: updatedWishListIds },
      });

      res.status(200).json({
        message: "Listing is removed from wish list",
        wishList: updatedWishList,
      });
    } else {
      const updatedWishListIds = [...wishList, listingId];
      const updatedWishList = await Promise.all(
        updatedWishListIds.map(async (id) => {
          const listing = await prisma.listing.findUnique({
            where: { id: parseInt(id) },
            include: { creator: true },
          });
          return listing;
        })
      );

      await prisma.user.update({
        where: { id: parseInt(userId) },
        data: { wishList: updatedWishListIds },
      });

      res.status(200).json({
        message: "Listing is added to wish list",
        wishList: updatedWishList,
      });
    }
  } catch (err) {
    console.log(err);
    res.status(500).json({ error: "Something went wrong" });
  }
});

/* GET PROPERTY LIST */
router.get("/:userId/properties", async (req, res) => {
  try {
    const { userId } = req.params;
    const properties = await prisma.listing.findMany({
      where: { creatorId: parseInt(userId) },
      include: { creator: true },
    });
    res.status(202).json(properties);
  } catch (err) {
    console.log(err);
    res
      .status(404)
      .json({ message: "Can not find properties!", error: err.message });
  }
});

/* GET RESERVATION LIST */
router.get("/:userId/reservations", async (req, res) => {
  try {
    const { userId } = req.params;
    const reservations = await prisma.listing.findMany({
      where: { creatorId: parseInt(userId) },
      include: { creator: true },
    });
    res.status(202).json(reservations);
  } catch (err) {
    console.log(err);
    res
      .status(404)
      .json({ message: "Can not find reservations!", error: err.message });
  }
});

module.exports = router;
