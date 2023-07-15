import React from 'react';
import { CircularProgress } from '@mui/material';

function Loader({size,color}) {
    return (
        <div style={{display: 'flex', justifyContent:'center'}}>
            <CircularProgress size={size} color={color}/>
        </div>
    )
}

export default Loader;
