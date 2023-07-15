import React, { useState } from "react";
import { Link, useHistory } from "react-router-dom";
import { Grid, Checkbox } from "@mui/material";
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import MDInput from "components/MDInput";
import MDButton from "components/MDButton";
import bgImage from "assets/images/login.jpg";
import { useFormik } from "formik";
import { signUpvalidationSchema } from "validator";
import { useMutation } from "react-query";
import { notifySuccess, notifyError } from "components/Messages";
import { login } from "services/Authentication.Services";
import { register } from "services/Authentication.Services";

function SignUp() {

  const navigate = useHistory()
  const [ loading, setLoading ]= useState('idle')
  const initState = {
    firstName: "",
    lastName: "",
    address: "",
    phone: "",
    email: "",
    password: "",
    confirmPassword: "",
  };

  const formik = useFormik({
    initialValues: initState,
     validationSchema: signUpvalidationSchema,
    onSubmit: (values) => {
       setLoading("pending")
      mutate(values);
    },
  });


  const { mutate } = useMutation(register, {
    onSuccess: (res) => {
      console.log(res,"response")
      notifySuccess("SignUp Successfully")
      setLoading("success");
      navigate.push("/login");
      let token = res.data.accessToken;
       let userDetail = JSON.stringify({
        id: res.data.user.id,
      });
      localStorage.setItem("user", userDetail);
      localStorage.setItem("token", token);
    },
    onError: (error) => {
      setLoading("error");
      notifyError(
        `${error?.response?.data?.error?.message
          ? error.response.data.error.message
          : "Something went wrong"
        }`
      );
    },
  });

  return (
    <MDBox
      width="100vw"
      height="100%"
      minHeight="100vh"
      bgColor="white"
      sx={{ overflow: "hidden" }}
    >
      <Grid
        container
      >
        <Grid item xs={12} lg={6}>
          <MDBox
            display={{ xs: "none", lg: "flex" }}
            width="calc(100% - 2rem)"
            height="calc(100vh - 2rem)"
            borderRadius="lg"
            ml={2}
            mt={2}
            sx={{ backgroundImage: `url(${bgImage})` }}
          />
        </Grid>
        <Grid item xs={11} sm={8} md={7} lg={4} xl={4} sx={{ mx: "auto" }}>
          <MDBox
            display="flex"
            flexDirection="column"
            justifyContent="center"
            height="100vh"
          >
            <MDBox py={3} px={3} textAlign="center">
              <>
                <MDBox mb={1} textAlign="center">
                  <MDTypography variant="h4" fontWeight="bold">
                    Join us today
                  </MDTypography>
                </MDBox>
                <MDTypography variant="body2" color="text">
                  Enter your email and password to register
                </MDTypography>
              </>
            </MDBox>
            <MDBox p={3}>
              <MDBox
                component="form"
                role="form"
                onSubmit={formik.handleSubmit}
              >
                <MDBox mb={2}>
                  <MDInput type="text" label="First Name"
                    value={formik.values.firstName}
                    id="firstName"
                    autoComplete="firstName"
                    onChange={formik.handleChange}
                    error={formik.touched.firstName && Boolean(formik.errors.firstName)}
                    helperText={formik.touched.firstName && formik.errors.firstName}
                    fullWidth />
                </MDBox>
                <MDBox mb={2}>
                  <MDInput type="text"
                    label="Last Name"
                    value={formik.values.lastName}
                    id="lastName"
                    autoComplete="lastName"
                    onChange={formik.handleChange}
                    error={formik.touched.lastName && Boolean(formik.errors.lastName)}
                    helperText={formik.touched.lastName && formik.errors.lastName}
                    fullWidth />
                </MDBox>
                <MDBox mb={2}>
                  <MDInput type="text" label="Address" value={formik.values.address}
                    id="address"
                    autoComplete="address"
                    onChange={formik.handleChange}
                    error={formik.touched.address && Boolean(formik.errors.address)}
                    helperText={formik.touched.address && formik.errors.address}
                    fullWidth />
                </MDBox>

                <MDBox mb={2}>
                  <MDInput type="number" label="Phone Number"
                    value={formik.values.phone}
                    id="phone"
                    autoComplete="phone"
                    onChange={formik.handleChange}
                    error={formik.touched.phone && Boolean(formik.errors.phone)}
                    helperText={formik.touched.phone && formik.errors.phone}
                    fullWidth />
                </MDBox>
                <MDBox mb={2}>
                  <MDInput
                    type="email"
                    label="Email"
                    value={formik.values.email}
                    id="email"
                    autoComplete="email"
                    onChange={formik.handleChange}
                    error={formik.touched.email && Boolean(formik.errors.email)}
                    helperText={formik.touched.email && formik.errors.email}
                    fullWidth
                  />
                </MDBox>
                <MDBox mb={2}>
                  <MDInput
                    type="password"
                    label="Password"
                    value={formik.values.password}
                    id="password"
                    autoComplete="password"
                    onChange={formik.handleChange}
                    error={formik.touched.password && Boolean(formik.errors.password)}
                    helperText={formik.touched.password && formik.errors.password}
                    fullWidth
                  />
                </MDBox>
                <MDBox mb={2}>
                  <MDInput
                    type="password"
                    label="Confirm Password"
                    value={formik.values.confirmPassword}
                    id="confirmPassword"
                    autoComplete="confirmPassword"
                    onChange={formik.handleChange}
                    error={formik.touched.confirmPassword && Boolean(formik.errors.confirmPassword)}
                    helperText={formik.touched.confirmPassword && formik.errors.confirmPassword}
                    fullWidth
                  />
                </MDBox>
                <MDBox display="flex" alignItems="center" ml={-1}>
                  <Checkbox />
                  <MDTypography
                    variant="button"
                    fontWeight="regular"
                    color="text"
                    sx={{ cursor: "pointer", userSelect: "none", ml: -1 }}
                  >
                    &nbsp;&nbsp;I agree the&nbsp;
                  </MDTypography>
                  <MDTypography
                    component="a"
                    href="#"
                    variant="button"
                    fontWeight="bold"
                    color="info"
                    textGradient
                  >
                    Terms and Conditions
                  </MDTypography>
                </MDBox>
                <MDBox mt={4} mb={1}>
                  <MDButton
                    type="submit"
                    variant="gradient"
                    color="info"
                    size="large"
                    fullWidth
                    isLoading={loading}
                  >
                    sign up
                  </MDButton>
                </MDBox>
                <MDBox mt={3} textAlign="center">
                  <MDTypography variant="button" color="text">
                    Already have an account?{" "}
                    <MDTypography
                      component={Link}
                      to="/login"
                      variant="button"
                      color="info"
                      fontWeight="medium"
                      textGradient
                    >
                      Sign In
                    </MDTypography>
                  </MDTypography>
                </MDBox>
              </MDBox>
            </MDBox>
          </MDBox>
        </Grid>
      </Grid>
    </MDBox>
  );
}

export default SignUp;
