"""processes
"""
import time

from .models import PlayerToTeamMembershipClaimProcess
from viewflow import flow
from viewflow.base import this, Flow

class PlayerToTeamMembershipClaimFlow(Flow):
    process_class = PlayerToTeamMembershipClaimProcess

    start = (
        flow.Start(
            flow.views.CreateProcessView,
            fields=['due_date','payment_due_date','player','team']
        ).Permission(
            auto_create=True
        ).Next(this.wait_until_claim_deadline_or_other_claim)
    )

    wait_until_claim_deadline_or_other_claim = (
        flow.Split(
        ).Next(this.wait_until_claim_deadline
        ).Next(this.wait_for_other_claim)
    )

    wait_until_claim_deadline = (
        flow.Handler(this.waituntilClaimDeadline)
    )

    def waituntilClaimDeadline(self,activation):
        time.sleep(10)

    wait_for_other_claim = (
        flow.Handler(this.waituntilClaimDeadline)
    )

    generate_receipts = (
        flow.Handler(lambda tmp: tmp
        ).Next(this.send_receipts)
    )

    send_receipts =(
        flow.Handler( lambda tmp: tmp
        ).Next(this.wait_until_payment_deadline_or_receipt_is_paid)
    )

    wait_until_payment_deadline_or_receipt_is_paid = (
        flow.Handler(lambda tmp: tmp
        ).Next(this.end)
    )
    end = flow.End()

