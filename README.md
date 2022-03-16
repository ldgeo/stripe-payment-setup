# Stripe - setup payment methods

Useful to generate a `checkout` session needed to save customers payment methods for recurring payments (in particular SEPA debits)


## Requirements

    poetry
    python >= 3.9

## Installation

    poetry install

## Config

Copy `.env.sample` to `.env` and customize it

## Launch the service

    poetry run stripe-setup-payment

Jump to [http://localhost:4242/](http://localhost:4242/)