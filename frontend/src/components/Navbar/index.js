import * as React from 'react';
import {AppBar,Box,Toolbar,IconButton,Typography,Menu,Container,Button,Tooltip,MenuItem} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import Avatar from '@mui/material/Avatar';
import MDBox from 'components/MDBox';
import {useHistory} from "react-router-dom";
import { useAuth } from 'context/AuthContext';

const pages = ['Home','About Us', 'Products', 'Pricing','Jobs','Buy','Log out'];


function Navbar() {
  const navigate = useHistory();
  const [anchorElNav, setAnchorElNav] = React.useState(null);
  const {logout} = useAuth()

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };

  

  const handleNavigation = async (e,page) => {
   if(page==='Buy'){
    navigate.push("/addcreditcard");
   }
   
  };


  return (
    <AppBar position="static" sx={{backgroundColor:"#0b0527"}}>
      <Container maxWidth="xl">
        <Toolbar disableGutters>
     <MDBox sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }}>
     <img src="https://analytickit.com/wp-content/uploads/2022/04/cropped-newlogo-small.png"  alt="logo" width="120px"/>

     </MDBox>
          {/* <AdbIcon sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }} /> */}
          <Typography
            variant="h6"
            noWrap
            component="a"
            href="/"
            sx={{
              mr: 2,
              display: { xs: 'none', md: 'flex' },
              textDecoration:'none',
              fontSize:'25px',
              fontFamily: '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: ' white',

            }}
          >
         Web Analytic
          </Typography>

          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="white"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={""}
              sx={{
                display: { xs: 'block', md: 'none' },
              }}
            >
              {pages.map((page) => (
                <MenuItem key={page} onClick={(e)=>handleNavigation(e,page)}>
                  <Typography textAlign="center">{page}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
          <MDBox sx={{ display: { xs: 'flex', md: 'none' }, mr: 1 }}>
        <img src="https://analytickit.com/wp-content/uploads/2022/04/cropped-newlogo-small.png"  alt="logo"  width="120px"/>

     </MDBox>

          <Typography
            variant="h5"
            noWrap
            component="a"
            href=""
            sx={{
              mr: 2,
              display: { xs: 'flex', md: 'none' },
              flexGrow: 1,
              textDecoration:'none',
              fontSize:'25px',
              fontFamily: '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: ' white',
            }}
          >
          Web Analytic
          </Typography>
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            {pages.map((page) => (
              <Button
                key={page}
                onClick={(e)=>handleNavigation(e,page)}
                color='white'
                sx={{ my: 2, color:'white', display: 'block',fontSize:"15px",fontWeight:400 }}
              >
                {page}
              </Button>
            ))}

            
          </Box>

          <Box sx={{ flexGrow: 0 }}>

              <IconButton  sx={{ p: 0 }}>
                <Avatar alt="S" src="/static/images/avatar/2.jpg" />
              </IconButton>


          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}
export default Navbar;