const express = require("express");
const router = express.Router();
const { PrismaClient } = require("@prisma/client");
const prisma = new PrismaClient();

/* CREATE BOOKING */
router.post("/create", async (req, res) => {
  try {
    const { customerId, hostId, listingId, startDate, endDate, totalPrice } =
      req.body;

    const newBooking = await prisma.booking.create({
      data: {
        customerId: parseInt(customerId),
        hostId: parseInt(hostId),
        listingId: parseInt(listingId),
        startDate,
        endDate,
        totalPrice: parseFloat(totalPrice),
      },
    });

    res.status(200).json(newBooking);
  } catch (err) {
    console.log(err);
    res
      .status(400)
      .json({ message: "Failed to create a new Booking!", error: err.message });
  }
});

module.exports = router;
