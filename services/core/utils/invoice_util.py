from services.core.models import Reservation, Invoice


def generateInvoice(id, fiscal_bill):
    try:
        reservation = Reservation.objects.get(id=id)
        if reservation.paid_off:

            Invoice.objects.create(reservation=reservation, fiscal_bill=fiscal_bill)

        else:
            raise Exception("Reservation has not been paid off. "
                            "You can generate deposit slip for initial payment.")
    except Reservation.DoesNotExist:
        raise Exception("Reservation with given id does not exist.")