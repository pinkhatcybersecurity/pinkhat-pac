resource "aws_lb_listener" "vulnerable_protocol" {
  load_balancer_arn = aws_lb.front_end.arn
  port              = "80"
  protocol          = "HTTP"
}

resource "aws_lb_listener" "mutual_authentication_ignore_cert" {
  load_balancer_arn = aws_lb.front_end.arn
  port              = "443"
  protocol          = "HTTPS"

  mutual_authentication = {
    ignore_client_certificate_expiry = true
  }
}
