require('dotenv').config();
require('dns').setServers(['8.8.8.8', '1.1.1.1']);
const mongoose = require('mongoose');
const User = require('../models/User');

(async () => {
  await mongoose.connect(process.env.MONGO_URI);

  const demo = [
    { name: 'Admin User', email: 'admin@earthscape.com', password: 'Admin@12345', role: 'admin' },
    { name: 'Analyst User', email: 'analyst@earthscape.com', password: 'Analyst@12345', role: 'analyst', assignedRegions: ['Asia', 'Europe'] },
  ];

  for (const u of demo) {
    const exists = await User.findOne({ email: u.email });
    if (!exists) {
      await User.create(u);
      console.log('Created:', u.email);
    } else {
      console.log('Already exists:', u.email);
    }
  }
  await mongoose.disconnect();
})();
