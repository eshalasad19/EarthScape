const router = require('express').Router();
const { listUsers, updateUser } = require('../controllers/userController');
const { protect } = require('../middleware/auth');
const { allowRoles } = require('../middleware/role');

router.use(protect, allowRoles('admin'));
router.get('/', listUsers);
router.patch('/:id', updateUser);

module.exports = router;
