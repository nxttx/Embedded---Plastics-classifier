# remove all the txt files in the directory
import os


def removeLabels(dir):
  images = os.listdir(dir)
  for image in images:
    if '.txt' in image:
      os.remove(os.path.join(dir, image))
    else :
      continue

    


if __name__ == "__main__":
    # dataset image directories
    root_dir = os.path.join("blok2", "conveyerAcquisition", "datasets")
    bag_dir = os.path.join(root_dir, "bag")
    bottle_dir = os.path.join(root_dir, "bottle")
    bottlecap_dir = os.path.join(root_dir, "bottlecap")
    fork_dir = os.path.join(root_dir, "fork")
    knife_dir = os.path.join(root_dir, "knife")
    pen_dir = os.path.join(root_dir, "pen")
    spoon_dir = os.path.join(root_dir, "spoon")
    styrofoam_dir = os.path.join(root_dir, "styrofoam")


    # remove labelfiles
    removeLabels(bag_dir)
    removeLabels(bottle_dir)
    removeLabels(bottlecap_dir)
    removeLabels(fork_dir)
    removeLabels(knife_dir)
    removeLabels(pen_dir)
    removeLabels(spoon_dir)
    removeLabels(styrofoam_dir)

    