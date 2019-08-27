import { PythonShell } from "python-shell";
import routes from "../routes";
import Rpa from "../models/Rpa";

let intervalObj;

// Home

export const home = async (req, res) => {
  res.render("home", { pageTitle: "Home", videos: [] });
};

export const postHome = async (req, res) => {
  const {
    user: { _id },
    body: { url, How, contact, Test }
  } = req;

  const newRpa = await Rpa.create({
    url,
    contact,
    Test
  });
  try {
    const options = {
      mode: "text",
      pythonPath: "C:/Users/user/Anaconda3/python.exe",
      pythonOptions: ["-u"],
      scriptPath: "./src",
      args: [url, How, contact, Test, _id]
    };
    const monitoring = opt => {
      PythonShell.run("Rpa.py", opt, (err, results) => {
        if (err) throw err;
        console.log("results: %j", results);
      });
    };
    intervalObj = setInterval(() => {
      monitoring(options);
    }, 60000);
  } catch (error) {
    console.log(error);
  }
  res.redirect(`/rpa${routes.checking}`);
};

export const getDashboard = (req, res) =>
  res.render("checking", { pageTitle: "Checking" });

export const postDashboard = async (req, res) => {
  clearInterval(intervalObj);
  res.redirect(routes.home);
};
