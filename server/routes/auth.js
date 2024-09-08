const router = require("express").Router();
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const multer = require("multer");
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "public/uploads/");
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  },
});

const upload = multer({ storage });

router.post("/register", upload.single("profileImage"), async (req, res) => {
  try {
    const { firstName, lastName, email, password } = req.body;

    const profileImage = req.file;

    if (!profileImage) {
      return res.status(400).send("No file uploaded");
    }

    /* path to the uploaded profile photo */
    const profileImagePath = profileImage.path;

    /* Check if user exists */
    const existingUser = await prisma.user.findUnique({ where: { email } });
    if (existingUser) {
      return res.status(409).json({ message: "User already exists!" });
    }

    /* Hash the password */
    const salt = await bcrypt.genSalt();
    const hashedPassword = await bcrypt.hash(password, salt);

    const newUser = await prisma.user.create({
      data: {
        firstName,
        lastName,
        email,
        password: hashedPassword,
        profileImagePath,
      },
    });

    res.status(200).json({ message: "User registered successfully!", user: newUser, success: true });
  } catch (err) {
    console.log(err);
    res.status(500).json({ success:true,message: "Registration failed!", error: err.message });
  }
});

router.post("/login", async (req, res) => {
  try {
    /* Take the information from the form */
    const { email, password } = req.body;
    /* Check if user exists */
    const user = await prisma.user.findUnique({ where: { email } });
    if (!user) {
      return res.status(404).json({ message: "User doesn't exist!" });
    }

    /* Compare the password with the hashed password */
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(400).json({ message: "Invalid Credentials!" });
    }

    /* Generate JWT token */
    const token = jwt.sign({ id: user.id }, "dain");
    delete user.password;

    res.status(200).json({ token, user, success: true });
  } catch (err) {
    console.log(err);
    res.status(500).json({ error: err.message });
  }
});

/* USER PASSWORD RESET */
router.post("/reset-password", async (req, res) => {
  try {
    /* Take the information from the form */
    const { email, password, code } = req.body;

    /* Check if user exists */
    const user = await prisma.user.findUnique({ where: { email } });
    if (!user) {
      return res.status(404).json({ message: "User not found!" });
    }

    /* Hash the new password */
    const salt = await bcrypt.genSalt();
    const hashedPassword = await bcrypt.hash(password, salt);

    /* Update user's password */
    const updatedUser = await prisma.user.update({
      where: { email },
      data: { password: hashedPassword },
    });

    /* Send a successful message */
    res.status(200).json({ message: "Password reset successfully!", success: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Password reset failed!", error: err.message });
  }
});

module.exports = router;
