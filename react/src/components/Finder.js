import React, {useState, useEffect} from 'react';
import './../App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Row, Container, Col } from 'react-bootstrap';
import Cookies from 'js-cookie';
import CustomNavbar from './Navbar'
import GallerySticker from './GallerySticker'

export default function Finder() {
  const [galleriesComp, setGalleriesComp] = useState([]);
  const [menuComponents, setMenuComponents] = useState([]);
  const [year, setYear] = useState('');
  const [result, setResult] = useState([]);
  const cookie = Cookies.get('csrftoken')

    //Modal open state
    const [state, setState] = useState(false);
    //Current loaded picture in modal
    const [current, setCurrent] = useState(null);
    const [picsList, setPicsList] = useState([]);
    const [pics, setPics] = useState([]);

    //Open image in full screen when vignette is clicked
    const toggleModal = (e, img) => {
    setCurrent(img)
    setState(true)
  };

  //Close image modal
  const closeModal = () => {
    setState(false)
  };

  //Goto next picture in modal
  const nextPicture = () => {
    console.log(pics)
    let nextId = pics.indexOf(current)+1;
    if(nextId == pics.length) nextId = 0
    setCurrent(pics[nextId]);
  };

  //Goto previous picture in modal
  const previousPicture = () => {
    let nextId = pics.indexOf(current)-1;
    if(nextId == -1) nextId = pics.length-1
    setCurrent(pics[nextId]);
  };

  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': Cookies.get('csrftoken') },
  };
  

  useEffect(() => {
    let picsDiv = []
    let picsTemp = []
    fetch('/api/associated_pics/', requestOptions)
          .then(res => res.json())
          .then(
            (result) => {
              for(const pic in result){
                picsTemp.push(result[pic].link + '/uploads/' + result[pic].file_full_name)
                picsDiv.push(
                <Col key={pic} xs="12" sm="6" md="4" lg="2">
                  <GallerySticker img={result[pic].link + '/uploads/' + result[pic].file_full_name}
                                  thumb={result[pic].link + '/thumbnails/' + result[pic].file_full_name}
                                  modal_func={toggleModal}/>
                </Col>
                )
              }
              setPicsList(picsDiv)
              setPics(picsTemp)
              console.log(picsTemp)
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
          <Row>
          <Col xs="12" sm="6" md="4" lg="2">
          <form method="POST" class="post-form" enctype="multipart/form-data">
            <input type="hidden" name="csrfmiddlewaretoken" value={cookie} />
            <input type='file' name='tronche'/>
            <button type="submit" className="login-button">Lancer la recherche</button>
          </form>
        </Col>
          </Row>
        </Container>
        <Container fluid>
          <Row className='g-1'>
            {picsList}
          </Row>
        </Container>

        {state && (
          <div className='pic-modal'>
            <ArrowBackIcon ref={ref2} onClick={previousPicture} className='arrow left-arrow'/>
            <ArrowForwardIcon ref={ref3} onClick={nextPicture} className='arrow right-arrow'/>
            <div className="pic-modal-nav">
              <span className='close' onClick={closeModal}>&times;</span>
              <a href={current} download={current}><span ref={ref4}><DownloadIcon className="download"/></span></a>
            </div>
            <div className='pic-modal-content'>
              <div ref={ref} className="img-browser">
                <img src={current} className='img-modal'/>
              </div>
            </div>
          </div>
          )
        }
      </>
    )
}
