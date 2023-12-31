import React, {useState} from 'react';
import './../App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const GallerySticker = (props) => {
    return(
            <div className="gallery-sticker" onClick={(event) => props.modal_func(event, props.img)}>
                <img loading='lazy' className="gallery-img" src={props.thumb} width="100%"/>
            </div>
    );
};

export default GallerySticker;