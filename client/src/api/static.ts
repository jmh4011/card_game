export const staticImage = (imagePath: string) => {
  return `/api/static/images/${imagePath}`;
}

export const characterImage = (imagePath: string) => {
  return staticImage(`/character/${imagePath}`);
};

export const fieldImage = () => {
  return staticImage("field.png")
}