import { Counter } from "../models/counter.model.js";

export const getNextClipId = async () => {
  const counter = await Counter.findOneAndUpdate(
    { name: "clipId" },
    { $inc: { value: 1 } },
    { new: true, upsert: true }
  );

  return counter.value;
};
