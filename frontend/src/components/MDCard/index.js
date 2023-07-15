
import PropTypes from "prop-types";
import Card from "@mui/material/Card";
import Grid from "@mui/material/Grid";
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import { useMaterialUIController } from "context";

function MDCard({ title, firstBlockHeader, firstBlockData, secondBlockHeader, secondBlockData, thirdBlockHeader,thirdBlockData }) {
    const [controller] = useMaterialUIController();
    const { darkMode } = controller;

    return (
        <Card sx={{border:"1px solid #f1ecec"}}>
            <MDBox p={2}>
                <Grid container>
                    <Grid item xs={7}>
                        <MDBox mb={2} lineHeight={1}>
                            <MDTypography
                                variant="button"
                                fontWeight="medium"
                                color="text"
                                textTransform="capitalize"
                            >
                                {title}
                            </MDTypography>
                        </MDBox>
                        <MDBox lineHeight={1}>
                            <MDTypography
                                variant="button"
                                fontWeight="regular"
                                color={darkMode ? "text" : "secondary"}
                            >
                                {firstBlockHeader}
                            </MDTypography>
                            <MDBox>
                                <MDTypography
                                    variant="button"
                                    color={darkMode ? "text" : "secondary"}
                                >
                                    {firstBlockData}
                                </MDTypography>
                            </MDBox>

                            <MDBox sx={{ mt: 2 }}>
                                <MDTypography
                                    variant="button"
                                    fontWeight="regular"
                                    color={darkMode ? "text" : "secondary"}
                                >
                                    {secondBlockHeader}
                                </MDTypography>

                                <MDBox>
                                   
                                        {secondBlockData}
                               
                                </MDBox>
                            </MDBox>


                            {/* <MDTypography variant="button" fontWeight="bold" color={percentage.color}>
                                {percentage.value}&nbsp;
                            </MDTypography> */}
                        </MDBox>
                        <MDBox sx={{mt:2}}>
                          <MDTypography
                                variant="button"
                                fontWeight="regular"
                                color={darkMode ? "text" : "secondary"}
                            >
                                {thirdBlockHeader}
                            </MDTypography>
                        </MDBox>
                        <MDBox>
                        {thirdBlockData}
                        </MDBox>
                    </Grid>

                </Grid>
            </MDBox>
        </Card>
    );
}



export default MDCard;
