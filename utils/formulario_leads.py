# utils/formulario_leads.py
# ============================================
# FORMULARIO DE LEADS + BOTONES CONTACTO - SAMU IA
# ============================================
# V4.0:
# - Botones WhatsApp + Llamar + Email antes del formulario
# - SVG inline (sin emojis en codigo, sin dependencias)
# - Estilos premium (gradientes, hover, cubic-bezier)
# - Formulario sigue guardando en crm_leads
# V3.0:
# - Usa SUPABASE_ANON_KEY (publishable)
# ============================================

import os
from dotenv import load_dotenv

load_dotenv()


SCRIPT_TEMPLATE = """
<script>
(function() {
    var SB_URL = "__SB_URL__";
    var SB_KEY = "__SB_KEY__";
    var PEDIDO_ID = "__PEDIDO_ID__";
    var TELEFONO = "__TELEFONO__";
    var NOMBRE_NEGOCIO = "__NOMBRE_NEGOCIO__";

    function getValueByName(form, name) {
        var el = form.querySelector('[name="' + name + '"]');
        if (el) return (el.value || "").trim();
        return "";
    }

    function getByType(form, type) {
        var el = form.querySelector('input[type="' + type + '"]');
        if (el) return (el.value || "").trim();
        return "";
    }

    function getTextarea(form) {
        var el = form.querySelector('textarea');
        if (el) return (el.value || "").trim();
        return "";
    }

    function asegurarCampoTelefono(form) {
        var existe = form.querySelector('[name="telefono"]') ||
                     form.querySelector('input[type="tel"]');
        if (existe) return;

        var emailInput = form.querySelector('input[type="email"]') ||
                         form.querySelector('[name="email"]');
        if (!emailInput) return;

        var wrapper = document.createElement('div');
        wrapper.style.marginTop = '12px';

        var input = document.createElement('input');
        input.type = 'tel';
        input.name = 'telefono';
        input.placeholder = 'Tu telefono (opcional)';
        input.style.cssText = 'width:100%;padding:12px 16px;border-radius:8px;border:1px solid #e2e8f0;font-size:1rem;font-family:inherit;outline:none;box-sizing:border-box;';

        wrapper.appendChild(input);

        var parent = emailInput.parentNode;
        if (parent && emailInput.nextSibling) {
            parent.insertBefore(wrapper, emailInput.nextSibling);
        } else if (parent) {
            parent.appendChild(wrapper);
        }
    }

    function limpiarFormulario(form) {
        form.removeAttribute('onsubmit');
        var inputs = form.querySelectorAll('input, textarea');
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].removeAttribute('required');
            inputs[i].removeAttribute('pattern');
        }
        var buttons = form.querySelectorAll('button, input[type="submit"]');
        for (var j = 0; j < buttons.length; j++) {
            buttons[j].removeAttribute('onclick');
        }
    }

    function mostrarMensaje(form, texto, esError) {
        var msg = form.querySelector('.lead-form-msg');
        if (!msg) {
            msg = document.createElement('div');
            msg.className = 'lead-form-msg';
            msg.style.cssText = 'margin-top:12px;padding:12px 16px;border-radius:8px;font-size:0.95rem;font-weight:500;';
            form.appendChild(msg);
        }
        if (esError) {
            msg.style.background = '#fee2e2';
            msg.style.color = '#991b1b';
            msg.style.border = '1px solid #fca5a5';
        } else {
            msg.style.background = '#d1fae5';
            msg.style.color = '#065f46';
            msg.style.border = '1px solid #6ee7b7';
        }
        msg.textContent = texto;
    }

    function buscarFormulario() {
        var forms = document.querySelectorAll('form');
        for (var i = 0; i < forms.length; i++) {
            if (forms[i].querySelector('input[type="email"]')) {
                return forms[i];
            }
        }
        return forms.length > 0 ? forms[0] : null;
    }

    function svgWA() {
        return '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.5 3.5A11 11 0 003.2 17.4L2 22l4.7-1.2a11 11 0 0016.3-9.8 11 11 0 00-2.5-7.5zm-8.5 17c-1.6 0-3.2-.4-4.6-1.2l-.3-.2-3.4.9.9-3.3-.2-.4a9.2 9.2 0 1117.1-4.9 9.2 9.2 0 01-9.5 9.1zm5-6.7c-.3-.1-1.6-.8-1.9-.9-.3-.1-.5-.1-.6.1s-.7.9-.9 1.1c-.2.2-.3.2-.6.1s-1.2-.4-2.2-1.4a8 8 0 01-1.5-1.9c-.2-.3 0-.4.1-.6.1-.1.3-.3.4-.5.1-.2.2-.3.2-.5 0-.2 0-.4-.1-.5 0-.1-.6-1.5-.8-2-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3a3 3 0 00-1 2.2 5.3 5.3 0 001.1 2.8c.1.2 2 3 4.7 4.2.7.3 1.2.5 1.6.6.7.2 1.3.2 1.7.1.5-.1 1.6-.7 1.9-1.3.2-.6.2-1.2.1-1.3-.1-.1-.3-.2-.5-.3z"/></svg>';
    }
    function svgTel() {
        return '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>';
    }
    function svgMail() {
        return '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V6a2 2 0 00-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>';
    }

    function inyectarBotonesContacto(ancla) {
        if (!TELEFONO) return;
        if (document.getElementById('samu-contact-buttons')) return;

        var telLimpio = TELEFONO.replace(/[^0-9+]/g, '');
        var nombre = NOMBRE_NEGOCIO || 'el negocio';
        var msgWA = encodeURIComponent('Hola, vengo de la web de ' + nombre + '. Quisiera mas informacion.');
        var waUrl = 'https://wa.me/' + telLimpio.replace('+', '') + '?text=' + msgWA;
        var telUrl = 'tel:' + telLimpio;

        var container = document.createElement('div');
        container.id = 'samu-contact-buttons';
        container.style.cssText = 'display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin:24px 0 32px 0;';

        var base = 'display:inline-flex;align-items:center;gap:8px;padding:14px 24px;border-radius:50px;font-weight:600;font-size:1rem;text-decoration:none;transition:all 0.3s cubic-bezier(0.4,0,0.2,1);box-shadow:0 4px 12px rgba(0,0,0,0.1);cursor:pointer;border:none;font-family:inherit;';

        var wa = document.createElement('a');
        wa.href = waUrl;
        wa.target = '_blank';
        wa.rel = 'noopener';
        wa.style.cssText = base + 'background:linear-gradient(135deg,#25D366,#128C7E);color:#fff;';
        wa.innerHTML = svgWA() + '<span>WhatsApp</span>';
        wa.onmouseenter = function() { this.style.transform = 'translateY(-3px)'; this.style.boxShadow = '0 8px 20px rgba(37,211,102,0.4)'; };
        wa.onmouseleave = function() { this.style.transform = 'translateY(0)'; this.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)'; };
        container.appendChild(wa);

        var tel = document.createElement('a');
        tel.href = telUrl;
        tel.style.cssText = base + 'background:linear-gradient(135deg,#3b82f6,#1e40af);color:#fff;';
        tel.innerHTML = svgTel() + '<span>Llamar</span>';
        tel.onmouseenter = function() { this.style.transform = 'translateY(-3px)'; this.style.boxShadow = '0 8px 20px rgba(59,130,246,0.4)'; };
        tel.onmouseleave = function() { this.style.transform = 'translateY(0)'; this.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)'; };
        container.appendChild(tel);

        var em = document.createElement('a');
        em.href = '#';
        em.style.cssText = base + 'background:linear-gradient(135deg,#8b5cf6,#6d28d9);color:#fff;';
        em.innerHTML = svgMail() + '<span>Email</span>';
        em.onmouseenter = function() { this.style.transform = 'translateY(-3px)'; this.style.boxShadow = '0 8px 20px rgba(139,92,246,0.4)'; };
        em.onmouseleave = function() { this.style.transform = 'translateY(0)'; this.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)'; };
        em.onclick = function(e) {
            e.preventDefault();
            if (ancla) {
                ancla.scrollIntoView({behavior: 'smooth', block: 'center'});
                setTimeout(function() {
                    var f = ancla.querySelector('input, textarea');
                    if (f) f.focus();
                }, 500);
            }
        };
        container.appendChild(em);

        var parent = ancla.parentNode;
        if (parent) {
            parent.insertBefore(container, ancla);
        } else {
            document.body.appendChild(container);
        }

        if (!ancla.id) ancla.id = 'samu-formulario';
    }

    function init() {
        var form = buscarFormulario();
        if (!form) {
            console.log('[SAMU IA] No hay formulario, solo botones.');
            if (TELEFONO) inyectarBotonesContacto(document.body);
            return;
        }

        asegurarCampoTelefono(form);
        limpiarFormulario(form);
        inyectarBotonesContacto(form);

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            e.stopPropagation();

            var nombre = getValueByName(form, 'nombre');
            var email = getValueByName(form, 'email') || getByType(form, 'email');
            var telefono = getValueByName(form, 'telefono') || getByType(form, 'tel');
            var mensaje = getValueByName(form, 'mensaje') || getTextarea(form);

            if (!nombre) {
                var firstText = form.querySelector('input[type="text"]');
                if (firstText) nombre = (firstText.value || "").trim();
            }

            if (!email || email.indexOf('@') === -1) {
                mostrarMensaje(form, 'Por favor ingresa un email valido.', true);
                return false;
            }

            var data = {
                pedido_web_id: PEDIDO_ID,
                nombre: nombre || 'Sin nombre',
                email: email,
                telefono: telefono || null,
                mensaje: mensaje || null,
                estado: 'nuevo',
                origen: 'formulario_web'
            };

            mostrarMensaje(form, 'Enviando...', false);

            fetch(SB_URL + '/rest/v1/crm_leads', {
                method: 'POST',
                headers: {
                    'apikey': SB_KEY,
                    'Authorization': 'Bearer ' + SB_KEY,
                    'Content-Type': 'application/json',
                    'Prefer': 'return=minimal'
                },
                body: JSON.stringify(data)
            })
            .then(function(r) {
                if (r.ok || r.status === 201) {
                    form.reset();
                    mostrarMensaje(form, 'Mensaje enviado. Te contactaremos pronto.', false);
                } else {
                    return r.text().then(function(t) {
                        console.error('[SAMU IA] Error:', t);
                        mostrarMensaje(form, 'Error al enviar. Intenta de nuevo.', true);
                    });
                }
            })
            .catch(function(err) {
                console.error('[SAMU IA] Error de red:', err);
                mostrarMensaje(form, 'Error de conexion. Intenta de nuevo.', true);
            });

            return false;
        }, true);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
</script>
"""


def inyectar_formulario_leads(html, pedido_web_id, telefono_negocio=None, nombre_negocio=None):
    """
    Inyecta script de captura de leads + botones WhatsApp/Tel/Email.

    Args:
        html: HTML completo de la web
        pedido_web_id: UUID del pedido
        telefono_negocio: telefono para WhatsApp/Llamar (opcional)
        nombre_negocio: nombre del negocio para el mensaje de WhatsApp (opcional)
    """
    if not html:
        return html

    if not pedido_web_id:
        print("[formulario_leads] Sin pedido_web_id, no se inyecta script")
        return html

    sb_url = os.getenv("SUPABASE_URL", "")
    sb_key = os.getenv("SUPABASE_ANON_KEY", "")

    if not sb_url or not sb_key:
        print("[formulario_leads] Faltan credenciales Supabase (URL o ANON_KEY)")
        return html

    if sb_key.startswith("sb_secret_") or "service_role" in sb_key:
        print("[formulario_leads] ERROR: Se detecto secret key. Usar SUPABASE_ANON_KEY.")
        return html

    def _js_escape(s):
        if not s:
            return ""
        return str(s).replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").replace("\r", "")

    script = SCRIPT_TEMPLATE
    script = script.replace("__SB_URL__", sb_url)
    script = script.replace("__SB_KEY__", sb_key)
    script = script.replace("__PEDIDO_ID__", str(pedido_web_id))
    script = script.replace("__TELEFONO__", _js_escape(telefono_negocio or ""))
    script = script.replace("__NOMBRE_NEGOCIO__", _js_escape(nombre_negocio or ""))

    html_lower = html.lower()
    idx = html_lower.rfind("</body>")

    if idx == -1:
        html_final = html + "\n" + script
        print("[formulario_leads] Script inyectado al final")
    else:
        html_final = html[:idx] + script + "\n" + html[idx:]
        print("[formulario_leads] Script inyectado antes de </body>")

    if telefono_negocio:
        print("[formulario_leads] Botones WhatsApp/Tel activados")
    else:
        print("[formulario_leads] Sin telefono, solo formulario email")

    return html_final


if __name__ == "__main__":
    print("=" * 60)
    print("TEST FORMULARIO LEADS V4.0")
    print("=" * 60)

    html_test = """<!DOCTYPE html>
<html><head><title>Test</title></head>
<body>
<form action="#" method="POST">
    <input type="text" name="nombre" placeholder="Nombre">
    <input type="email" name="email" placeholder="Email">
    <textarea name="mensaje" placeholder="Mensaje"></textarea>
    <button type="submit">Enviar</button>
</form>
</body></html>"""

    resultado = inyectar_formulario_leads(
        html_test,
        "test-pedido-123",
        telefono_negocio="+573214090873",
        nombre_negocio="Panaderia Los Tres Amigos",
    )

    print(f"HTML original:  {len(html_test)} chars")
    print(f"HTML final:     {len(resultado)} chars")
    print(f"Tiene script:   {'SI' if '<script>' in resultado else 'NO'}")
    print(f"Tiene botones:  {'SI' if 'samu-contact-buttons' in resultado else 'NO'}")
    print(f"Tiene WhatsApp: {'SI' if 'wa.me' in resultado else 'NO'}")
    print("=" * 60)