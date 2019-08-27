import multer from "multer";
import routes from "./routes";

const multerAvatar = multer({ dest: "uploads/avatars/" });

export const localsMiddleware = (req, res, next) => {
  res.locals.siteName = "KT - RPA";
  res.locals.routes = routes;
  res.locals.loggedUser = req.user || null;
  next();
};

export const onlyPublic = (req, res, next) => {
  if (req.user) {
    res.redirect(routes.home);
  } else {
    next();
  }
};

export const onlyPrivate = (req, res, next) => {
  if (req.user) {
    next();
  } else {
    res.redirect(routes.login);
  }
};

export const uploadAvatar = multerAvatar.single("avatar");
