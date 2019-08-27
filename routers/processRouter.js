import express from "express";
import routes from "../routes";
import { getDashboard, postDashboard } from "../controllers/processController";
import { onlyPrivate } from "../middlewares";

const processRouter = express.Router();

// Dashboard

processRouter.get(routes.checking, onlyPrivate, getDashboard);
processRouter.post(routes.checking, onlyPrivate, postDashboard);

export default processRouter;
