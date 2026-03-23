import { useEffect, useState } from 'react';
import { Container, Typography, List, ListItem, ListItemText, Button, Dialog, DialogTitle, DialogContent } from '@mui/material';
// import QRCode from 'qrcode.react';
import api from '../api';

export default function Profile({ user }) {
  const [tickets, setTickets] = useState([]);
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [qrOpen, setQrOpen] = useState(false);

  useEffect(() => {
    const fetchTickets = async () => {
      const res = await api.get('/user/me'); // предположим, что возвращает пользователя с билетами
      setTickets(res.data.tickets);
    };
    fetchTickets();
  }, []);

  const handleShowQR = (ticket) => {
    setSelectedTicket(ticket);
    setQrOpen(true);
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4">Мои билеты</Typography>
      <List>
        {tickets.map((ticket) => (
          <ListItem key={ticket.id} divider>
            <ListItemText primary={ticket.event_title} secondary={`Дата: ${ticket.event_date}`} />
            <Button variant="outlined" onClick={() => handleShowQR(ticket)}>
              Показать QR
            </Button>
          </ListItem>
        ))}
      </List>

      <Dialog open={qrOpen} onClose={() => setQrOpen(false)}>
        <DialogTitle>QR-код билета</DialogTitle>
        <DialogContent sx={{ display: 'flex', justifyContent: 'center' }}>
          {/* {selectedTicket && (
            <QRCode value={JSON.stringify({ ticketId: selectedTicket.id, userId: user?.id })} size={200} />
          )} */}
        </DialogContent>
      </Dialog>
    </Container>
  );
}