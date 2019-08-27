import mongoose from "mongoose";

const RpaSchema = new mongoose.Schema({
  url: {
    type: String,
    required: "File URL is required"
  },
  contact: {
    type: String,
    required: "Title is required"
  },
  Test: {
    type: String,
    required: "Title is required"
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

const model = mongoose.model("RPA", RpaSchema);
export default model;
