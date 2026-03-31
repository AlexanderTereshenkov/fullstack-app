import { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  Grid
} from '@mui/material';
import api from '../api';

export default function Profile() {
  const [user, setUser] = useState(null);
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [ticketsLoading, setTicketsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await api.get('/user/me');
        setUser(response.data);
      } catch (err) {
        console.error(err);
        setError(err.response?.data?.detail || 'Не удалось загрузить профиль');
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, []);

  useEffect(() => {
    const fetchTickets = async () => {
      try {
        const response = await api.get('/user/me/tickets');
        setTickets(response.data);
      } catch (err) {
        console.error(err);
      } finally {
        setTicketsLoading(false);
      }
    };
    fetchTickets();
  }, []);

  if (loading) {
    return (
      <Container sx={{ mt: 4, textAlign: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  if (!user) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="warning">Пользователь не найден</Alert>
      </Container>
    );
  }

  return (
    <Container sx={{ mt: 4 }}>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>
            Мой профиль
          </Typography>
          <Typography variant="body1">
            <strong>ID:</strong> {user.id}
          </Typography>
          <Typography variant="body1">
            <strong>Email:</strong> {user.email}
          </Typography>
          <Typography variant="body1">
            <strong>Роль:</strong> {user.role === 'admin' ? 'Администратор' : 'Пользователь'}
          </Typography>
          <Typography variant="body1">
            <strong>Дата регистрации:</strong>{' '}
            {new Date(user.created_at).toLocaleDateString()}
          </Typography>
        </CardContent>
      </Card>

      <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>
        Мои билеты
      </Typography>

      {ticketsLoading ? (
        <CircularProgress />
      ) : tickets.length === 0 ? (
        <Alert severity="info">У вас пока нет билетов</Alert>
      ) : (
        <Grid container spacing={2}>
          {tickets.map((ticket) => (
            <Grid item xs={12} md={6} key={ticket.id}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6">{ticket.title}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {new Date(ticket.date).toLocaleString()}
                  </Typography>
                  <Typography variant="body2">{ticket.location}</Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
}