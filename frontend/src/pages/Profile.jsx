import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  Button,
  IconButton
} from '@mui/material';
import { QrCodeScanner as QrCodeIcon } from '@mui/icons-material'; // если используете Material Icons
import { QRCodeSVG } from 'qrcode.react';
import api from '../api';

export default function Profile() {
  const [user, setUser] = useState(null);
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [ticketsLoading, setTicketsLoading] = useState(true);
  const [error, setError] = useState('');
  const [openQrDialog, setOpenQrDialog] = useState(false);
  const [selectedTicket, setSelectedTicket] = useState(null);

  const navigate = useNavigate();

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

  const handleOpenQr = (ticket) => {
    setSelectedTicket(ticket);
    setOpenQrDialog(true);
  };

  const handleCloseQr = () => {
    setOpenQrDialog(false);
    setSelectedTicket(null);
  };

  if (loading) {
    return (
      <Container sx={{ mt: 4, textAlign: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    navigate('/login')
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
                  <IconButton 
                    onClick={() => handleOpenQr(ticket)} 
                    sx={{ mt: 1 }}
                    color="primary"
                  >
                    <QrCodeIcon />
                  </IconButton>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Модальное окно с QR-кодом */}
      <Dialog open={openQrDialog} onClose={handleCloseQr}>
        <DialogTitle>QR-код билета</DialogTitle>
        <DialogContent sx={{ textAlign: 'center' }}>
          {selectedTicket && (
            <>
              <QRCodeSVG 
                value={`Билет #${selectedTicket.id}\n
                Мероприятие: ${selectedTicket.title}\n
                Дата: ${new Date(selectedTicket.date).toLocaleString()}\n
                Место: ${selectedTicket.location}`}
                size={200}
                level="H"
              />
              <Typography variant="caption" display="block" sx={{ mt: 2 }}>
                Покажите этот код при входе на мероприятие.
              </Typography>
            </>
          )}
          <Button onClick={handleCloseQr} sx={{ mt: 2 }} variant="contained">
            Закрыть
          </Button>
        </DialogContent>
      </Dialog>
    </Container>
  );
}