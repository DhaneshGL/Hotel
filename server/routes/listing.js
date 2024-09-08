const router = require("express").Router();
const { PrismaClient } = require("@prisma/client");
const prisma = new PrismaClient();
const multer = require("multer");

/* Configuration Multer for File Upload */
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "public/uploads/"); 
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);  
  },
});

const upload = multer({ storage });

/* CREATE LISTING */
router.post("/create", upload.array("listingPhotos"), async (req, res) => {
  try {
    const {
      creator,
      category,
      type,
      streetAddress,
      aptSuite,
      city,
      province,
      country,
      guestCount,
      bedroomCount,
      bedCount,
      bathroomCount,
      amenities,
      title,
      description,
      highlight,
      highlightDesc,
      price,
    } = req.body;

    const listingPhotos = req.files;
    if (!listingPhotos) {
      return res.status(400).send("No file uploaded.");
    }
    const listingPhotoPaths = listingPhotos.map((file) => file.path);

    const newListing = await prisma.listing.create({
      data: {
        creatorId: Number(creator),
        category,
        type,
        streetAddress,
        aptSuite,
        city,
        province,
        country,
        guestCount: Number(guestCount),
        bedroomCount: Number(bedroomCount),
        bedCount: Number(bedCount),
        bathroomCount: Number(bathroomCount),
        amenities: JSON.parse(amenities),
        listingPhotoPaths,
        title,
        description,
        highlight,
        highlightDesc,
        price: Number(price),
      },
    });

    res.status(200).json(newListing);
  } catch (err) {
    res
      .status(409)
      .json({ message: "Fail to create Listing", error: err.message });
    console.log(err);
  }
});

/* GET LISTINGS BY CATEGORY */
router.get("/", async (req, res) => {
  const qCategory = req.query.category;

  try {
    let listings;
    if (qCategory) {
      listings = await prisma.listing.findMany({
        where: {
          category: qCategory,
        },
        include: {
          creator: true,
        },
      });
    } else {
      listings = await prisma.listing.findMany({
        include: {
          creator: true,
        },
      });
    }

    res.status(200).json(listings);
  } catch (err) {
    res
      .status(404)
      .json({ message: "Fail to fetch listings", error: err.message });
    console.log(err);
  }
});

/* GET LISTINGS BY SEARCH */
router.get("/search/:search", async (req, res) => {
  const { search } = req.params;
  try {
    let listings = [];

    if (search === "all") {
      listings = await prisma.listing.findMany({
        include: {
          creator: true,
        },
      });
    } else {
      listings = await prisma.listing.findMany({
        where: {
          OR: [
            { category: { contains: search, mode: "insensitive" } },
            { title: { contains: search, mode: "insensitive" } },
          ],
        },
        include: {
          creator: true,
        },
      });
    }

    res.status(200).json(listings);
  } catch (err) {
    res
      .status(404)
      .json({ message: "Fail to fetch listings", error: err.message });
    console.log(err);
  }
});

router.get("/:listingId", async (req, res) => {
  try {
    const { listingId } = req.params;
    const listing = await prisma.listing.findUnique({
      where: { id: Number(listingId) },
      include: {
        creator: true,
      },
    });

    if (!listing) {
      return res.status(404).json({ message: "Listing not found" });
    }

    res.status(202).json(listing);
  } catch (err) {
    res
      .status(404)
      .json({ message: "Listing can not found!", error: err.message });
  }
});

module.exports = router;
