package org.opendreambox.dms;

import de.endrullis.utils.logging.LoggingUtils;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import javax.servlet.ServletException;
import javax.servlet.jsp.JspPage;
import javax.servlet.jsp.HttpJspPage;
import java.io.*;
import java.net.ServerSocket;
import java.util.Map;
import java.util.ArrayList;
import java.util.logging.Logger;

/**
 * Manages receiver clients (Dreambox) and sender clients (any webbrowser).
 */
public class DreamboxMessageServer extends HttpServlet {
	/** Logger. */
	private Logger logger = Logger.getLogger(DreamboxMessageServer.class.getName());


	enum Action { none, receiver, message, question }

	public static final int PORT = 8184;
	public static ConnectionManager connectionManager;

	public DreamboxMessageServer() {
		LoggingUtils.initLogManager("/logging.properties");
	}

	public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
		if (connectionManager == null) {
			logger.severe("test");
			connectionManager = new ConnectionManager(new ServerSocket(PORT));
		}

	  PrintWriter out = response.getWriter();

		if (request.getParameter("action") == null) {
			response.sendRedirect("index.html");
			return;
		}

		Action action = Action.valueOf(request.getParameter("action"));

		if (action == Action.receiver) {
			response.setContentType("text/txt");
			out.write("" + PORT);
			return;
		}

		response.setContentType("text/html");

		boolean missingAttribute = false;
		for (Object o : request.getParameterMap().entrySet()) {
			Map.Entry<String,String[]> entry = (Map.Entry<String,String[]>) o;
			if (entry.getValue().length > 0)
				request.setAttribute(entry.getKey(), entry.getValue()[0]);
		}
		
		String password = request.getParameter("password");
		String message = request.getParameter("message");

		if (password == null || password.equals("")) {
			request.setAttribute("passwordMissing", true);
			missingAttribute = true;
		}

		Receiver receiver = connectionManager.getReceiver(password);
		if (receiver == null) {
			request.setAttribute("error", "Wrong password!");
		}

		logger.info("action: " + action);

		switch (action) {
			case message:
				if (message == null || message.equals("")) {
					request.setAttribute("messageMissing", true);
					missingAttribute = true;
				}

				if (missingAttribute || receiver == null) {
					getServletContext().getRequestDispatcher("/SendMessage.jsp").forward(request,response);
					return;
				}

				if (receiver != null) {
					try {
						BufferedReader r = new BufferedReader(new InputStreamReader(new ByteArrayInputStream(message.getBytes())));
						String text = "";
						String line;
						while ((line = r.readLine()) != null) {
							text += line + "\n";
						}

						receiver.sendMessage(text.trim());
						request.setAttribute("status", "Message sent :)");
					} catch (Exception e) {
						request.setAttribute("error", "Message failed: " + e.getMessage());
					}
					getServletContext().getRequestDispatcher("/SendMessage.jsp").forward(request,response);
					return;
				}
				break;
			case question:
				if (message == null || message.equals("")) {
					request.setAttribute("messageMissing", true);
					missingAttribute = true;
				}

				if (missingAttribute || receiver == null) {
					getServletContext().getRequestDispatcher("/SendQuestion.jsp").forward(request,response);
					return;
				}

				if (receiver != null) {
					try {
						BufferedReader r = new BufferedReader(new InputStreamReader(new ByteArrayInputStream(message.getBytes())));
						String text = "";
						ArrayList<String> answers = new ArrayList<String>();
						String line;
						while ((line = r.readLine()) != null) {
							if (line.startsWith("-")) {
								break;
							}
							text += line + "\n";
						}

						if (line == null) {
							request.setAttribute("messageMissing", true);
							getServletContext().getRequestDispatcher("/SendQuestion.jsp").forward(request,response);
							return;
						}

						answers.add(line.substring(1).trim());
						while ((line = r.readLine()) != null) {
							answers.add(line.substring(1).trim());
						}

						String answer = receiver.sendQuestion(text, answers);

						request.setAttribute("status", "Question sent :)");
						request.setAttribute("answer", answer);
					} catch (Exception e) {
						request.setAttribute("error", "Message failed: " + e.getMessage());
					}
					getServletContext().getRequestDispatcher("/SendQuestion.jsp").forward(request,response);
					return;
				}
				break;
		}

	  HttpSession session = request.getSession(true);

	  out.println("<html>");
	  out.println("<head>");
	  out.println("  <title>DreamboxMessageServer</title>");
	  out.println("</head>");
	  out.println("<body>");
	  out.println("  " + action);
		out.flush();

		try {
			Thread.sleep(5000);
		} catch (InterruptedException e) {
		}

		out.println("<br>Bla");
		out.println("</body>");
		out.println("</html>");
	}

	public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
	  doGet(request, response);
	}

	private static <T> T sessionGet(HttpSession session, String key, T defaultValue) {
	  T value = (T) session.getAttribute(key);
	  if(value == null) { session.setAttribute(key, defaultValue); return defaultValue; }
	  return value;
	}

	@Override
	public void destroy() {
		connectionManager.close();
	}
}
