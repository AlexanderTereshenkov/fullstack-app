import { useEffect, useState } from 'react';
import { Container, Grid, Card, CardContent, Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import api from '../api';

export default function Events() {
  const [events, setEvents] = useState([]);
  const navigate = useNavigate();
  const user = localStorage.getItem('user');

  useEffect(() => {
    const fetchEvents = async () => {
      const res = await api.get('/events/');
      setEvents(res.data);
    };
    fetchEvents();
  }, []);

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        События
      </Typography>
      {user === 'admin' && (
        <Button variant="contained" sx={{ mb: 2 }} onClick={() => navigate('/admin/upload-poster')}>
          Добавить событие
        </Button>
      )}
      <Grid container spacing={3}>
        {events.map((event) => (
          <Grid item xs={12} key={event.id}>
            <Card sx={{ cursor: 'pointer' }} onClick={() => navigate(`/events/${event.id}`)}>
              <CardContent>
                <Typography variant="h6">{event.title}</Typography>
                <Typography color="textSecondary">{event.date}</Typography>
                <Typography>{event.location}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}