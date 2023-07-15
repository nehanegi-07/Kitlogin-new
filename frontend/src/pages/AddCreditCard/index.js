import React, { useState } from 'react'
import { Card } from '@mui/material'
import MDBox from 'components/MDBox'
import MDButton from 'components/MDButton'
import MDInput from 'components/MDInput'
import MDTypography from 'components/MDTypography'
import { useFormik } from 'formik'
import { creditCardvalidationSchema } from 'validator'
import { useHistory} from 'react-router-dom'


function AddCreditCard() {
    const navigate=useHistory()
    const [loading, setLoading] = useState("idle")
  
    const initState = {
        email: "",
        cardHolderName: "",
        cardNumber: "",
        expiryYear: "",
        expiryMonth: ""
    }

    const formik = useFormik({
        initialValues: initState,
         validationSchema: creditCardvalidationSchema,
        onSubmit: (values) => {
            setLoading("pending")
            navigate.push("/")
        },
    });

   
    return (
        <>
      
        <MDBox sx={{ width: "100vw", height: "100vh", display: "flex",flexDirection:"column", alignItems: "center", justifyContent: "center"}}>
            <MDBox sx={{pb:1}}>
            <img src="https://dpa.analytickit.com/static/assets/analytickit-logo-cloud-S37G2V6B.svg" alt="logo" width="420px" height="100px"/>
          </MDBox>
            <Card sx={{ border: "1px solid #dad1d1" }}>
            <MDBox py={3} px={3} textAlign="center">
          
                <MDBox mb={1} textAlign="center">
                  <MDTypography variant="h4" fontWeight="bold">
                  Enter your Credit Card Detail
                  </MDTypography>
                </MDBox>
             
        
            </MDBox>
                <MDBox pt={4} pb={3} px={3}>
                    <MDBox component="form" role="form" onSubmit={formik.handleSubmit}>
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
                                type="text"
                                label="Card Holder's Name"
                                value={formik.values.cardHolderName}
                                id="cardHolderName"
                                autoComplete="cardHolderName"
                                onChange={formik.handleChange}
                                error={formik.touched.cardHolderName && Boolean(formik.errors.cardHolderName)}
                                helperText={formik.touched.cardHolderName && formik.errors.cardHolderName}
                                fullWidth
                            />
                        </MDBox>
                        <MDBox mb={2}>
                            <MDInput
                                type="text"
                                label="Card Number"
                                value={formik.values.cardNumber}
                                id="cardNumber"
                                autoComplete="cardNumber"
                                onChange={formik.handleChange}
                                error={formik.touched.cardNumber && Boolean(formik.errors.cardNumber)}
                                helperText={formik.touched.cardNumber && formik.errors.cardNumber}
                                fullWidth
                            />
                        </MDBox>

                        <MDBox mb={2} display="flex" gap={{ xs: 2, md: 4 }}>
                            <MDBox mb={2} display="flex" gap={{ xs: 2, md: 4 }}>
                                <MDInput
                                    width={{ md: 200 }}
                                    type="text"
                                    label="Expiry Month"
                                    value={formik.values.expiryMonth}
                                    id="expiryMonth"
                                    autoComplete="expiryMonth"
                                    onChange={formik.handleChange}
                                    error={formik.touched.expiryMonth && Boolean(formik.errors.expiryMonth)}
                                    helperText={formik.touched.expiryMonth && formik.errors.expiryMonth}
                                />

                                <MDInput
                                    width={{ md: 200 }}
                                    type="text"
                                    label="Expiry Year"
                                    value={formik.values.expiryYear}
                                    id="expiryYear"
                                    autoComplete="expiryYear"
                                    onChange={formik.handleChange}
                                    error={formik.touched.expiryYear && Boolean(formik.errors.expiryYear)}
                                    helperText={formik.touched.expiryYear && formik.errors.expiryYear}
                                />
                            </MDBox>

                            <MDInput
                                width={{ md: 700 }}
                                type="text"
                                label="CVV Code"
                                value={formik.values.cvc}
                                id="cvc"
                                autoComplete="cvc"
                                onChange={formik.handleChange}
                                error={formik.touched.cvc && Boolean(formik.errors.cvc)}
                                helperText={formik.touched.cvc && formik.errors.cvc}
                            />
                        </MDBox>

                        <MDBox mt={4} mb={1} >
                            <MDButton  color="info" type="submit" fullWidth isLoading={loading}>
                                Save
                            </MDButton>
                        </MDBox>

                    </MDBox>
                </MDBox>
            </Card>
        </MDBox>
        </>
    )
}

export default AddCreditCard
