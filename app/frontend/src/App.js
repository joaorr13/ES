import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Row, Col, Typography, Layout, Input, Button, Spin, Card, message } from 'antd';
import './App.css';

const { Title } = Typography;
const { Header, Content } = Layout;

const App = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [inputState, setInputState] = useState(true);
  const [result, setResult] = useState(null);
  const [messageApi, contextHolder] = message.useMessage();
  const canvasRef = useRef(null);

  useEffect(() => {
    if(result){
      createCanvas();
    }
}, [result]);

  function createCanvas() {
    const image = new Image();
    const faces = result.faces;

    image.onload = () => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');

        const scaleFactorWidth = (window.innerWidth * 0.35) / image.width;
        const scaleFactorHeight = (window.innerHeight * 0.5) / image.height;

        canvas.width = scaleFactorWidth * image.width;
        canvas.height = scaleFactorHeight * image.height;

        ctx.drawImage(image, 0, 0, canvas.width, canvas.height);

        for (let i = 0; i < faces.length; i++) {
            let face = faces[i];
            let coordinates = face.coordinates;

            ctx.strokeStyle = '#00B295';
            ctx.lineWidth = 3;

            let left = coordinates.x * scaleFactorWidth;
            let upper = coordinates.y * scaleFactorHeight;
            let right = coordinates.width * scaleFactorWidth;
            let lower = coordinates.height * scaleFactorHeight;

            ctx.beginPath();
            ctx.rect(left, upper, right - left, lower - upper);
            ctx.stroke();

            ctx.font = `1.5vw Arial`;
            ctx.textAlign = 'center';
            ctx.strokeStyle = 'black';
            ctx.lineWidth = 1;
            ctx.strokeText(face.entityName, left + (right - left) / 2, upper - 10);
            ctx.fillStyle = '#00B295';
            ctx.fillText(face.entityName, left + (right - left) / 2, upper - 10);
        }
    };
    image.src = result.url
}

  const handleRecognize = async () => {
    if (!url.trim()) {
      messageApi.error('Please enter an image URL');
      return;
    }

    // Basic URL validation
    try {
      new URL(url);
    } catch (error) {
      messageApi.error('Please enter a valid URL');
      return;
    }

    try {
      setLoading(true);
      setInputState(false);
      const response = await axios.post('http://localhost:3001/recognize', { url });
      setLoading(false);
      if(response.data.status == 'Inaccessible'){
        setInputState(true)
        messageApi.error("URL Inaccessible")
      }else if (response.data.faces.length == 0){
        setInputState(true)
        messageApi.error("No faces identified in image")
        
      }else{
        setInputState(false)
        setResult(response.data);  
      }
    } catch (error) {
      console.error('Error:', error);
      messageApi.error('Failed to process the image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout >
      {contextHolder}
       <Header
      style={{
        display: 'flex',
        alignItems: 'center', // Centers vertically
        justifyContent: 'flex-start', // Aligns text to the left
        background: '#0B132B',
        paddingLeft: '16px', // Add padding for spacing
      }}
    >
      <Title
        style={{ 
          color: 'white', 
          margin: 0, 
          cursor: 'pointer', // Adds pointer cursor on hover
          transition: 'color 0.3s' // Smooth color transition on hover
        }}
        onClick={() => {
          setInputState(true);
          setLoading(false);
          setResult(null);
        }}
        onMouseEnter={(e) => (e.target.style.color = '#277EB6')} // Change color on hover
        onMouseLeave={(e) => (e.target.style.color = 'white')} // Reset color on mouse leave
      >
        Recognition App
      </Title>
      
    </Header>
      
    <Content className="p-8" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
          {inputState && (
            <Col span={11} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
            <Card bordered={false} style={{ width: '100%'}}>
              <Title level={3} style={{ color: '#277EB6', fontFamily: 'Roboto, sans-serif'}}>Face Recognition</Title>
              <p style={{ fontSize: 'smaller', fontFamily: 'Roboto, sans-serif', color:'0x808080' }}>Submit an image and Uncover Who's in Them!</p>
              <div style={{ maxHeight: '30vh', overflowY: 'auto' }}>
                    <Input
                      type="url"
                      placeholder="Enter Image URL (.png, .jpg, .jpeg)"
                      value={url}
                      onChange={(event) => {setUrl(event.target.value)}}
                      style={{ display: 'block', marginBottom: '1vh' }}
                    />
              </div>
              <Button type="primary"onClick={handleRecognize} style={{ marginTop: '2vh', backgroundColor: '#277EB6', borderColor: '#277EB6'}}>
                      Find Faces
              </Button>
            </Card>
          </Col>  
          )}
          

          {loading && (
            <div className="flex justify-center my-8">
              <Spin size="large" />
            </div>
          )}

          {result && (
            <Row gutter={45} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', width:'100vw' }}>


            {/*-------  Left ----------------------------------------------------*/}
               <Col span={11} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column'}}>
   
                   
                       <Title level={2} style={{ color: '#277EB6', fontFamily: 'Roboto, sans-serif'}}>Results</Title>
                       <Card bordered={false} style={{ width: '90%', justifyContent: 'center', alignItems: 'center' }}>
                           <div style={{ width: '100%'}}>
                               <canvas ref={canvasRef} style={{ width: '35vw', height: '50vh', borderRadius: '15px' }}></canvas>
                           </div>
                       </Card>
                   
               </Col>
   
                {/*-------  Right ----------------------------------------------------*/}
               <Col span={10} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column'}}>
   
                    <Title level={2} style={{ color: '#277EB6', fontFamily: 'Roboto, sans-serif'}}>Identified Faces</Title>
                    <Card bordered={false} style={{ width: '90%', justifyContent: 'center', alignItems: 'center', maxHeight: '55vh', overflowY: 'auto' }}>
   
                       <p style={{ fontFamily: 'Roboto, sans-serif', color:'#1C2541', fontSize:'medium', fontWeight:'bolder' }}>
                           {result.faces.length === 1 ? 
                               '1 Face was Identified' : 
                               `${result.faces.length} Faces were Identified`}
                       </p>
    
                            {/*-------  Face Cards ----------------------------------------------------*/}
                           {result.faces.map((person, index) => (
                               <Card bordered={true} style={{ width: '100%', justifyContent: 'center', alignItems: 'center', paddingBottom:'1px'}}>
                               <div key={person.entityId} style={{ paddingLeft: '60px'}}>
                                   <div>
                                       {/*-------  Text ----------------------------------------------------*/}
                                       <div id={`player-${index}`} style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'flex-start', alignItems: 'center' }}>
                                        <p>
                                            <Title level={4} style={{ color: '#277eb6', fontFamily: 'Roboto, sans-serif'}}>Face {index + 1}: </Title>
                                            <span style={{ fontFamily: 'Roboto, sans-serif', fontSize: 'medium', color:'#1C2541'}}>{person.entityName}</span>
                                        </p>
                                       </div>
                                   </div>
                               </div>
                               </Card>
                           ))}
                       </Card>
               </Col>
           </Row>
          )}

      </Content>
    </Layout>
  );
};

export default App;