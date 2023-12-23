import React, {useState, useEffect} from 'react';
import './../App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Container, Row, Col} from 'react-bootstrap';
import Cookies from 'js-cookie';
import CustomNavbar from './Navbar'
import YouTube from 'react-youtube';

export default function VideoGallery(props) {
  const [result, setResult] = useState([]);

  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': Cookies.get('csrftoken')
    },
  };
  useEffect(() => {
    fetch('/api/videos/get/', requestOptions)
      .then(res => res.json())
      .then(
        (result) => {
            let menuCompTemp = []
            for (const video in result) {
                var id = '';
                var url = result[video].video_url
                url = url.replace(/(>|<)/gi, '').split(/(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)/);
                if (url[2] !== undefined) {
                    id = url[2].split(/[^0-9a-z_\-]/i);
                    id = id[0];
                }
                else {
                    id = url;
                }
                menuCompTemp.push(
                    <Row style={{marginTop: '40px', marginBottom: '40px'}} className="justify-content-md-center">
                        <Col md="auto">
                            <YouTube videoId={id}/>
                        </Col>
                    </Row>)
            }
            setResult(menuCompTemp)
        },
        (error) => {
          console.log(error)
        }
      );
  }, [])

  return (
      <>
        <CustomNavbar/>
        <Container>
            {result}
        </Container>
      </>
    )
}
