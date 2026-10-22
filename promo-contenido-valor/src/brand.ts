// Identidad de marca — placeholder basado en los presets locales de Manuel Toro
// (newsroom financiero: navy / off-white / dorado). Reemplazar con los hex reales
// del perfil @conmanueltoro cuando estén disponibles.
export const COLORS = {
  navy: "#0B1F3A",
  navyDeep: "#061427",
  offWhite: "#F4F1EA",
  gold: "#D4A947",
  goldSoft: "#E9C978",
  muted: "#8FA3BF",
};

export const FONTS = {
  display: "Inter Display",
  body: "Inter",
};

export const HANDLE = "@conmanueltoro";

export type Post = { label: string; title: string; body: string };

// Contenido placeholder: 3 consejos en la voz de la marca.
export const POSTS: Post[] = [
  {
    label: "Publicación 01",
    title: "El precio de China no es tu costo.",
    body: "Sumá flete, aduana y margen antes de poner el precio de venta.",
  },
  {
    label: "Publicación 02",
    title: "Respondé en menos de 5 minutos.",
    body: "Después de eso, el cliente ya le escribió a otro.",
  },
  {
    label: "Publicación 03",
    title: "No vendas todo. Vendé lo que escala.",
    body: "Menos catálogo, más rotación, más margen.",
  },
];

export const HOOK = {
  top: "3 datos que",
  mid: "nadie te dice",
  bottom: "antes de vender.",
};
export const CTA = { line1: "Seguí", line2: "para más contenido de valor" };
