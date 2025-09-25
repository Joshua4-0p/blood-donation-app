import React from "react";
import { render } from "@testing-library/react-native";
import App from "../app/index";

describe("App", () => {
  it("renders onboarding tagline", () => {
    const { getByText } = render(<App />);
    expect(
      getByText("Your chance to finally be the hero you have always dreamed to be")
    ).toBeTruthy();
  });
});
