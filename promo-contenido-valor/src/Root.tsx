import { Composition } from "remotion";
import { Promo } from "./Promo";
import "./fonts";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Promo"
      component={Promo}
      durationInFrames={300}
      fps={30}
      width={1080}
      height={1920}
    />
  );
};
