defmodule Dispatcher do
  use Matcher
  define_accept_types [
    html: [ "text/html", "application/xhtml+html" ],
    json: [ "application/json", "application/vnd.api+json" ]
  ]

  @any %{}
  @json %{ accept: %{ json: true } }
  @html %{ accept: %{ html: true } }

  define_layers [ :static, :services, :fall_back, :not_found ]

  # In order to forward the 'themes' resource to the
  # resource service, use the following forward rule:
  #
  # match "/themes/*path", @json do
  #   Proxy.forward conn, path, "http://resource/themes/"
  # end
  #
  # Run `docker-compose restart dispatcher` after updating
  # this file.

  match "/people/*path" do
    Proxy.forward conn, path, "http://resource/person/"
  end

  match "/sparql/*path" do
    Proxy.forward conn, path, "http://triplestore:8890/sparql/"
  end

  match "/aanduidingsobject/*path" do
    Proxy.forward conn, path, "http://resource/aanduidingsobject/"
  end

  match "/aanduidingsobject1/*path" do
    Proxy.forward conn, path, "http://resource/aanduidingsobject1/"
  end

  match "/aanvraag/*path" do
    Proxy.forward conn, path, "http://resource/aanvraag/"
  end

  match "/aanvrager/*path" do
    Proxy.forward conn, path, "http://resource/aanvrager/"
  end

  match "/contactpersoon/*path" do
    Proxy.forward conn, path, "http://resource/contactpersoon/"
  end

  match "/*path", @html do
    Proxy.forward conn, path, "http://frontend/"
  end

  match "/*_", %{ layer: :not_found } do
    send_resp( conn, 404, "Route not found." )
  end
end
