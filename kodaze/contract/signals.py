from .models import Contract
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import create_payment_date_task, demo_satis_quantityi_task

from restAPI.v1.utils.ocean_contract_pdf_create import (
    okean_create_contract_pdf, 
    okean_contract_pdf_canvas, 
    ocean_installment_create_contract_pdf,
    ocean_installment_contract_pdf_canvas
)

from restAPI.v1.utils.magnus_contract_pdf_create import (
    magnus_create_contract_pdf,
    magnus_contract_pdf_canvas,
    magnus_installment_create_contract_pdf,
    magnus_installment_contract_pdf_canvas
)

@receiver(post_save, sender=Contract)
def create_payment_date(sender, instance, created, **kwargs):
    if created:
        instance_id = instance.id
        create_payment_date_task.delay(instance_id, True)

@receiver(post_save, sender=Contract)
def create_and_add_pdf_to_contract(sender, instance, created, **kwargs):
    if created:
        print("Signal işə düşdü")
        
        okean = "OCEAN"
        magnus = "MAGNUS"

        if instance.office.company.name == okean:
            contract_pdf_canvas_list = okean_contract_pdf_canvas(
                contract=instance, customer=instance.customer
            )
            contract_pdf = okean_create_contract_pdf(contract_pdf_canvas_list, instance)
        elif instance.office.company.name == magnus:
            contract_pdf_canvas_list = magnus_contract_pdf_canvas(
                contract=instance, customer=instance.customer
            )
            contract_pdf = magnus_create_contract_pdf(contract_pdf_canvas_list, instance)
        
        instance.pdf = contract_pdf
        instance.save()
    
@receiver(post_save, sender=Contract)
def create_and_add_pdf_to_contract_installment(sender, instance, created, **kwargs):
    if created:
        print("Signal işə düşdü")

        okean = "OCEAN"
        magnus = "MAGNUS"

        if instance.office.company.name == okean:
            contract_pdf_canvas_list = ocean_installment_contract_pdf_canvas(
                contract=instance
            )
            contract_pdf = ocean_installment_create_contract_pdf(contract_pdf_canvas_list, instance)
        elif instance.office.company.name == magnus:
            contract_pdf_canvas_list = magnus_installment_contract_pdf_canvas(
                contract=instance
            )
            contract_pdf = magnus_installment_create_contract_pdf(contract_pdf_canvas_list, instance)
        instance.pdf2 = contract_pdf
        instance.save()


@receiver(post_save, sender=Contract)
def demo_satis_quantityi(sender, instance, created, **kwargs):
    if created:
        instance_id = instance.id
        demo_satis_quantityi_task.delay(instance_id)