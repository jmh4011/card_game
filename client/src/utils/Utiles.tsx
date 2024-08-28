import React, { useEffect, useState } from "react";

export const styleVibration = (
  setVibration: (vibration: boolean) => void,
  t: number = 400
) => {
  setVibration(true);
  setTimeout(function () {
    setVibration(false);
  }, t);
};
