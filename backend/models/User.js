import mongoose from 'mongoose';

const UserSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  gpa: { type: Number, default: 0 },
  preferredCountry: { type: String },
  targetUniversity: { type: String },
  familyIncome: { type: Number },
  createdAt: { type: Date, default: Date.now }
});

export const User = mongoose.model('User', UserSchema);
