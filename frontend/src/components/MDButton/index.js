import { forwardRef } from "react";

// prop-types is a library for typechecking of props
import PropTypes from "prop-types";

// Custom styles for MDButton
import MDButtonRoot from "components/MDButton/MDButtonRoot";
// Material Dashboard 2 PRO React contexts
import { useMaterialUIController } from "context";
import { CircularProgress } from "@mui/material";

const MDButton = forwardRef(
  (
    {
      color,
      variant,
      size,
      isLoading,
      circular,
      loaderColor,
      iconOnly,
      children,
      ...rest
    },
    ref
  ) => {
    const [controller] = useMaterialUIController();
    const { darkMode } = controller;

    return (
      <MDButtonRoot
        {...rest}
        ref={ref}
        color="primary"
        variant={variant === "gradient" ? "contained" : variant}
        size={size}
        ownerState={{ color, variant, size, circular, iconOnly, darkMode }}
      >
        {isLoading === "pending" ? (
          <CircularProgress size={19} color={loaderColor} />
        ) : (
          children
        )}
      </MDButtonRoot>
    );
  }
);

// Setting default values for the props of MDButton
MDButton.defaultProps = {
  size: "medium",
  variant: "contained",
  color: "white",
  circular: false,
  iconOnly: false,
  loaderColor: "white",
};

// Typechecking props for the MDButton
MDButton.propTypes = {
  size: PropTypes.oneOf(["small", "medium", "large"]),
  variant: PropTypes.oneOf(["text", "contained", "outlined", "gradient"]),
  loaderColor: PropTypes.oneOf([
    "white",
    "primary",
    "secondary",
    "info",
    "success",
    "warning",
    "error",
    "light",
    "dark",
  ]),
  color: PropTypes.oneOf([
    "white",
    "primary",
    "secondary",
    "info",
    "success",
    "warning",
    "error",
    "light",
    "dark",
    "lighDark",
  ]),
  circular: PropTypes.bool,
  iconOnly: PropTypes.bool,
  children: PropTypes.node.isRequired,
};

export default MDButton;
